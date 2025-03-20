// TODO
// src/concatenate and src/create fasta should not need to load vamb

// Requires a FASTA parser in Rust, w. sequence validation and
// OPTIONAL name validation (concat may rename)

// Also gzip de/compressor

use std::borrow::Cow;

use numpy::{PyReadwriteArray1, PyReadwriteArray2};
use pyo3::prelude::*;

// Make lookup table for ACGT -> 0123.
// Ambiguous nucleotides are 4.
// Invalid nucleotides are assumed not to exist, as they should have been
// checked for on the Python side.
const fn make_lut() -> [u8; 256] {
    let mut lut = [4u8; 256];
    let mut i: usize = 0;
    while i < 128 {
        match i as u8 {
            b'A' | b'a' => lut[i] = 0,
            b'C' | b'c' => lut[i] = 1,
            b'G' | b'g' => lut[i] = 2,
            b'T' | b't' | b'U' | b'u' => lut[i] = 3,
            _ => (),
        };
        i += 1;
    }
    lut
}

const LUT: [u8; 256] = make_lut();

/// Count fourmers in a byte array. Takes a NumPy array of u32 counts, and a byte array.
/// The bytes must only contain IUPAC nucleotides. The counts must be zeroed, and have length 256.
#[pyfunction]
fn kmercounts(mut counts: PyReadwriteArray1<u32>, bytes: Cow<[u8]>) {
    let mut kmer = 0u32;
    let mut countdown = 3;
    let mask = 0x000000ff;
    let counts_slice = counts.as_slice_mut().unwrap();

    if counts_slice.len() != 256 {
        panic!("Counts array has wrong length");
    }

    for &byte in bytes.iter() {
        // Safety: A u8 cannot be out of bounds for a length 256 array
        let &val = unsafe { LUT.get_unchecked(byte as usize) };
        if val == 4 {
            countdown = 4;
        }

        kmer = ((kmer << 2) | (val as u32)) & mask;

        if countdown == 0 {
            // Safety: We just masked the lower 8 bits, so kmer is in the range 0..=255.
            // Since we checked before the loop that counts has length 256, this must be inbounds.
            unsafe {
                *counts_slice.get_unchecked_mut(kmer as usize) += 1;
            }
        } else {
            countdown -= 1;
        }
    }
}

// Given a slice of bool values, iterates over Range<usize> where the bools are true,
// in order.
struct ContiguousTrueRanges<'a> {
    mask: &'a [bool],
    pos: usize,
}

impl<'a> ContiguousTrueRanges<'a> {
    fn new(mask: &'a [bool]) -> Self {
        Self { mask, pos: 0 }
    }
}

// TODO: We could make this faster by using the bytemuck crate to cast the bools to a &[u8],
// then use memchr.
impl Iterator for ContiguousTrueRanges<'_> {
    type Item = std::ops::Range<usize>;

    fn next(&mut self) -> Option<Self::Item> {
        let len = self.mask.len();

        if self.pos >= len {
            return None;
        }

        // Find next true
        let n_until_start = match self.mask[self.pos..].iter().position(|x| *x) {
            Some(i) => i,
            None => {
                self.pos = len;
                return None;
            }
        };

        // Find next false
        let end: usize = match self.mask[self.pos + n_until_start + 1..]
            .iter()
            .position(|x| !*x)
        {
            Some(i) => i,
            None => {
                let res = self.pos + n_until_start..len;
                self.pos = len;
                return Some(res);
            }
        };

        let span = self.pos + n_until_start..self.pos + n_until_start + end + 1;
        self.pos = span.end + 1;
        Some(span)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_contiguous_true_ranges() {
        let mask = vec![false, true, true, false, false, true, true, true, false];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![1..3, 5..8]);

        let mask = vec![false, true, true, true];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![1..4]);

        let mask = vec![true, true, true];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![0..3]);

        let mask = vec![false, false, false];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![]);

        let mask = vec![true, false, true, false, true];
        let ranges: Vec<_> = ContiguousTrueRanges::new(&mask).collect();
        assert_eq!(ranges, vec![0..1, 2..3, 4..5]);
    }
}

/// Given matrix, a 2D NumPy array of float32, and a mask, a 1D NumPy array of bool, where
/// the length of mask is equal to the number of rows in matrix, this function works like
/// matrix[mask], except in-place.
/// It returns the number of filled rows. The matrix must then be truncated on the Python side.
#[pyfunction]
fn overwrite_matrix(mut matrix: PyReadwriteArray2<f32>, mask: PyReadwriteArray1<bool>) -> usize {
    let nrow = matrix.as_array().shape()[0];
    let ncol = matrix.as_array().shape()[1];

    let mask_slice = mask.as_slice().unwrap();

    if nrow != mask_slice.len() {
        panic!("Matrix and mask must have the same number of rows");
    }

    let matrix = matrix.as_slice_mut().unwrap();
    let mut write_row_index: usize = 0;

    for range in ContiguousTrueRanges::new(mask.as_slice().unwrap()) {
        // If range.start is 0, then it copies into its own position needlessly
        if range.start != 0 {
            matrix.copy_within(range.start * ncol..range.end * ncol, write_row_index * ncol);
        }
        write_row_index += range.len();
    }

    write_row_index
}

/// Low-level functionality of Vamb which can't easily be done in Python
#[pymodule]
fn vambcore(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(kmercounts, m)?)?;
    m.add_function(wrap_pyfunction!(overwrite_matrix, m)?)?;
    Ok(())
}
