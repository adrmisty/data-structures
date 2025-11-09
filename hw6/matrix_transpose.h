/*
 *  This file is #include'd inside the definition of a matrix class
 *  like this:
 *
 *  	class ClassName {
 *          // Number of rows and columns of the matrix
 *          unsigned N;
 *
 *          // Swap elements (i1,j1) and (i2,j2)
 *          void swap(unsigned i1, unsigned j1, unsigned i2, unsigned j2);
 *
 *          // Your code
 *          #include "matrix_transpose.h"
 *      }
 */

/*
    NOTES/#TODOs
    -----

    > use pseudocode of recursive transposition approach 
    on slide 52 https://ktiml.mff.cuni.cz/~fink/teaching/data_structures_I/tutorial_01.pdf.

    [-] check minimum and maximum matrix sizes (segmentation fault when out of bounds) 
    [-] take into account that even if square, dims can be even/odd
        # however should work for both power/non-power of two so shouldnt be too different?
        # with (m-h)
    [-] literally do as in the pseudocode? think it will get much more complicated/convoluted
    if i start adding extra checks or unnecessary code that will make it harder to debug/follow
*/

void transpose() {
    /*
    Transposes a matrix A into A^T,
    starting from index 0 and with dimensions NxN.
    */
    transpose_on_diagonal(0, N);
}

void transpose_on_diagonal(unsigned i, unsigned m) {
    /*
    Recursively transposes a square matrix on the main diagonal.
    Does nothing if matrix too small/too big.

    Params: i (x-coordinate to transpose from), m (order of the matrix)
    */

    if (m <= 1 || i >= N) return;  

    unsigned h = m / 2;

    // a. recursive transposition over the diagonal
    transpose_on_diagonal(i, h);            // A11, h:1, top-left
    transpose_on_diagonal(i + h, m - h);    // A22, h:1, bottom-right

    // b. recursive transposition + swap:
    // same i:i+h and h:m-h as diagonal transp
    transpose_and_swap(
        i, 
        i + h, 
        h, 
        m - h);
}

void transpose_and_swap(unsigned i, unsigned j, unsigned m, unsigned n) {
    /*
    Helper recursive function that swaps a matrix of size m × n starting at position (i, j) 
    with a matrix of size n × m starting at position (j, i).
    Does nothing if matrix too small/too big.

    Params: i,j (positions to transpose/swap from) and m,n (orders of the matrices, mxn and nxm)
    */

    if (m <= 0 || n <= 0 || i >= N || j >= N) return;

    // a. swap A12 <-> A21, bottom-left <-> top-right
    if (m == 1 && n == 1) {
        if (i < N && j < N) {
            swap(i, j, j, i);
        }
        return;
    }

    // b. recursive transposition + swaps
    unsigned mh = m / 2;
    unsigned nh = n / 2;

    // left trans+swap
    transpose_and_swap( // A11 <-> B11
        i,      j, 
        mh,     nh);                  
    transpose_and_swap( // A12 <-> B21
        i,      j + nh, 
        mh,     n - nh);   

    // right trans+swap
    transpose_and_swap( // A21 <-> B12
        i + mh,     j, 
        m - mh,     nh);         
    transpose_and_swap( // A22 <-> B22
        i + mh,     j + nh, 
        m - mh,     n - nh);
}
