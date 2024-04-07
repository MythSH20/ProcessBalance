#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MATRIX_SIZE 1400

// Function to generate a random value between 0 and 100
int randomValue()
{
    return rand() % 101; // Random number between 0 and 100
}

// Function to allocate memory for a matrix
int **allocateMatrix(int rows, int cols)
{
    int **matrix = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++)
    {
        matrix[i] = (int *)malloc(cols * sizeof(int));
    }
    return matrix;
}

// Function to free memory allocated for a matrix
void freeMatrix(int **matrix, int rows)
{
    for (int i = 0; i < rows; i++)
    {
        free(matrix[i]);
    }
    free(matrix);
}

// Function to generate a random matrix
void generateRandomMatrix(int **matrix, int rows, int cols)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            matrix[i][j] = randomValue();
        }
    }
}

// Function to print a matrix
void printMatrix(int **matrix, int rows, int cols)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

// Function to multiply two matrices
void multiplyMatrices(int **matrix1, int **matrix2, int **result, int rows1, int cols1, int cols2)
{
    for (int i = 0; i < rows1; i++)
    {
        for (int j = 0; j < cols2; j++)
        {
            result[i][j] = 0;
            for (int k = 0; k < cols1; k++)
            {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
}

int main()
{
    srand(time(NULL)); // Seed the random number generator

    int **matrix1 = allocateMatrix(MATRIX_SIZE, MATRIX_SIZE);
    int **matrix2 = allocateMatrix(MATRIX_SIZE, MATRIX_SIZE);
    int **result = allocateMatrix(MATRIX_SIZE, MATRIX_SIZE);

    // Generate random matrices
    generateRandomMatrix(matrix1, MATRIX_SIZE, MATRIX_SIZE);
    generateRandomMatrix(matrix2, MATRIX_SIZE, MATRIX_SIZE);

    // Multiply matrices
    clock_t start_time = clock();
    multiplyMatrices(matrix1, matrix2, result, MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE);
    clock_t end_time = clock();

    // Calculate elapsed time
    double elapsed_time = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;

    // Print elapsed time
    printf("Matrix multiplication time: %f seconds\n", elapsed_time);

    // Free allocated memory
    freeMatrix(matrix1, MATRIX_SIZE);
    freeMatrix(matrix2, MATRIX_SIZE);
    freeMatrix(result, MATRIX_SIZE);

    return 0;
}
