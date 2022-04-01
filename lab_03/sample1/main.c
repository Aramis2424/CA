
#include <stdio.h>
#include <stdlib.h>

#define FILE_NAME "table.txt"

#define OK 0
#define FILE_ERROR -1
#define SOME_ERROR -2

typedef struct
{
    int count;
    double *x_arr;
    double *y_arr;
} table_r;


double F(double x)
{
    return x * x;
}

void  free_table(table_r *table)
{
    if (table == NULL)
    {
        return;
    }

    table->count = 0;

    if (table->x_arr)
    {
        free(table->x_arr);
    }

    if (table->y_arr)
    {
        free(table->y_arr);
    }
}


int read_table(FILE *f, table_r *table)
{
    if (f == NULL)
    {
        return FILE_ERROR;
    }

    int rc = OK, count;\

    rc = fscanf(f, "Count %d", &count);
    if (rc != 1 || count <= 0)
    {
        printf("Error while reading file.\n");
        
        return FILE_ERROR;
    }

    table->count = count;
    table->x_arr = calloc(count, sizeof(double));
    table->y_arr = calloc(count, sizeof(double));

    rc = 2;
    for (int i = 0; i < count && rc == 2; ++i)
    {
        rc = fscanf(f, "%lf%lf", table->x_arr + i, table->y_arr + i);
    }

    if (rc != 2)
    {
        printf("Error while reading file.\n");
        
        return FILE_ERROR;
    }

    return OK;
}


void print_table(table_r table)
{
    printf("--------------|---------------\n");
    printf("%10s    |%10s    ", "X", "Y");
    printf("\n");
    printf("--------------|---------------\n");

    for (int i = 0; i < table.count; i++)
    {
        printf("% 10lf    |% 10lf    \n", *(table.x_arr + i), *(table.y_arr + i));
        printf("--------------|---------------\n");
    }
}


int found_in_x(double x, table_r table)
{
    int find = 0;

    for (int i = 0; i < table.count; ++i)
    {
        if (x < table.x_arr[i])
        {
            find = i;
            break;
        }
    }

    return find;
}

// Сплайн используется для нахождения приближенного 
// значения функции, указанной в табличном представлении.
int interp_spline(table_r table, double x_arg)
{
    if (table.count <= 0)
    {
        printf("Some error with table.\n");

        return SOME_ERROR;
    }

    double *arr_a = calloc(sizeof(double), table.count);
    double *arr_b = calloc(sizeof(double), table.count);
    double *arr_d = calloc(sizeof(double), table.count);
    double *arr_A = calloc(sizeof(double), table.count);
    double *arr_B = calloc(sizeof(double), table.count);
    double *arr_D = calloc(sizeof(double), table.count);
    double *arr_F = calloc(sizeof(double), table.count);
    double *arr_C = calloc(sizeof(double), table.count);
    double *arr_Kci = calloc(sizeof(double), table.count);
    double *arr_Etta = calloc(sizeof(double), table.count);
    double *arr_Hn = calloc(sizeof(double), table.count);

    for (int i = 1; i < table.count; ++i)
    {
        arr_Hn[i] = table.x_arr[i] - table.x_arr[i - 1];
    }

    //  Прмямой ход (1 этап алгоритма)
    for (int i = 2; i < table.count; ++i)
    {
        arr_A[i] = arr_Hn[i - 1];
        arr_D[i] = arr_Hn[i];

        arr_B[i] = (-2) * (arr_A[i] + arr_D[i]);

        arr_F[i] = (-3) * ((table.y_arr[i] - table.y_arr[i - 1]) / arr_Hn[i] - 
                           (table.y_arr[i] - table.y_arr[i - 2]) / arr_Hn[i - 1]);

        arr_Kci[i + 1] = arr_D[i] / (arr_B[i] - arr_A[i] * arr_Kci[i]);
        arr_Etta[i + 1] = (arr_A[i] * arr_Etta[i] + arr_F[i]) / (arr_B[i] - arr_A[i] * arr_Kci[i]);
    }

    // Обратный ход (2 этап)

    for (int i = table.count - 2; i >= 2; i--)
    {
        arr_C[i] = arr_Kci[i + 1] * arr_C[i + 1] + arr_Etta[i + 1];
    }

    for (int i = table.count - 1; i > 0; i--)
    {
        arr_a[i] = table.y_arr[i - 1];
        arr_d[i] = (arr_C[i + 1] - arr_C[i]) / (3 * arr_Hn[i]);
        arr_b[i] = (table.y_arr[i] - table.y_arr[i - 1]) / arr_Hn[i] - 
                   (1 / 3) * arr_Hn[i] * (arr_C[i + 1] + 2 * arr_C[i]);
    }

    //  Нахождение значения по заданному X
    int found_ix = found_in_x(x_arg, table);

    double x = x_arg - table.x_arr[found_ix - 1];
    double x2 = x * x;
    double x3 = x * x * x;

    double result = arr_a[found_ix] + arr_b[found_ix] * x + arr_C[found_ix] * x2 +
                    arr_d[found_ix] * x3;

    printf("Для заданного значения X (%lf) соответствует следующее значение Y = %lf\n\n", x_arg, result);
    
    free(arr_Hn);
    free(arr_A);
    free(arr_B);
    free(arr_D);
    free(arr_F);
    free(arr_C);
    free(arr_a);
    free(arr_b);
    free(arr_d);
    free(arr_Kci);
    free(arr_Etta);

    return OK;
}


int main()
{
    FILE *f = fopen(FILE_NAME, "r");
    if (f == NULL)
    {
        printf("Error while reading file.\n");
        
        return FILE_ERROR;
    }

    table_r table = { 0 };

    read_table(f, &table);
    fclose(f);

    print_table(table);
    
    printf("Введите X для поиска Y: ");
    double x_arg;
    int rc = scanf("%lf", &x_arg);

    if (rc != 1)
    {
        printf("Ошибка при считывания данного.\n");

        return SOME_ERROR;
    }

    interp_spline(table, x_arg);
    printf("Действительное значение Y(x), для x = %lf, равно %lf\n\n", x_arg, F(x_arg));

    return OK;
}
