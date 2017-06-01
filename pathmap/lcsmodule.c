#include <Python.h>


/**
 * Calculates the longest common substring
 * between two strings
 *
 * @param needle - The string to search for in hay
 * @param hay    - The string being searched
 *
 * @return An array of [0: length, 1: end_pos] 
 *		   where 
 *			length = length of the longest common substring
 *			end_pos = the end index of the longest common substring in needle
 * */
int *_lcs(char *needle, char *hay) {
    int strlen1 = strlen(needle);
    int strlen2 = strlen(hay);
    int len = (strlen1 < strlen2) ? strlen2 : strlen1;
    int i, j, k;
    int longest = 0;
    int **ptr = (int **)malloc(2 * sizeof(int *));
    static int *ret;
    ret = (int *)malloc((len + 3) * sizeof(int));
    for (i = 0; i < 2; i++)
        ptr[i] = (int *)calloc(strlen2, sizeof(int));

    ret[1] = -1;
    for (i = 0; i < strlen1; i++) {
        memcpy(ptr[0], ptr[1], strlen2 * sizeof(int));
        for (j = 0; j < strlen2; j++) {
            if (tolower(needle[i]) == tolower(hay[j])) {
                if (i == 0 || j == 0) {
                    ptr[1][j] = 1;
                } else {
                    ptr[1][j] = ptr[0][j-1] + 1;
                }
                if (ptr[1][j] > longest) {
                    longest = ptr[1][j];
                    k = 1;
                }
                if (ptr[1][j] == longest) {
                    ret[k++] = i;
                    ret[k] = -1;
                }
            } else {
                ptr[1][j] = 0;
            }
        }
    }
    for (i = 0; i < 2; i++)
        free(ptr[i]);
    free(ptr);
    /* store the maximum length in ret[0] */
    ret[0] = longest;
    return ret;
}


static PyObject*
lcs(PyObject* self, PyObject* args)
{
    char *s1;
    char *s2;
    char *substr;
    
    int i, longest, *results;
    i = 0;

    if (!PyArg_ParseTuple(args, "ss", &s1, &s2))
        return NULL;

    results = _lcs(s1, s2);


    if ((longest = results[0]) == 0) {
        Py_INCREF(Py_None);
        return Py_None;
    }

    substr = (char *)malloc(longest+1 * sizeof(char));
    memset(substr, '\0', longest+1);

    while (results[++i] != -1) {
        strncpy(substr, &s1[results[i] - longest + 1], longest);
    }

    PyObject *ret = Py_BuildValue("s", substr, longest+1);

	free(substr);
    return ret;
}


static PyMethodDef LCSMethods[] = {
    {"longest_common_substring", lcs, METH_VARARGS, "Calculate the longest common substring between two strings"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "lcs",     /* m_name */
        "",  /* m_doc */
        -1,                  /* m_size */
        LCSMethods    /* m_methods */
    };
#endif

static PyObject *
moduleinit(void)
{
    PyObject *m;

#if PY_MAJOR_VERSION >= 3
    m = PyModule_Create(&moduledef);
#else
    m = Py_InitModule3("lcs",
                        LCSMethods, "");
#endif
    return m;
}

#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC
PyInit_lcs(void)
{
    return moduleinit();
}
#else
PyMODINIT_FUNC
initlcs(void)
{
    moduleinit();
}
#endif
