#include <Python.h>


int *_lcs(char *s, char *t) {
    int strlen1 = strlen(s);
    int strlen2 = strlen(t);
    int len = (strlen1 < strlen2) ? strlen2 : strlen1;
    int i, j, k;
    int longest = 0;
    int **ptr = (int **)malloc(2 * sizeof(int *));
    static int *ret;
    /*
     * Maximum length of the return list (considering intermediate steps).
     * It is the maximum length of the source strings + 1 (worst-case
     * intermediate length) + the value of the longest match + the
     * terminator value (-1).
     */
    ret = (int *)malloc((len + 3) * sizeof(int));
    for (i = 0; i < 2; i++)
        ptr[i] = (int *)calloc(strlen2, sizeof(int));

    ret[1] = -1;
    for (i = 0; i < strlen1; i++) {
        memcpy(ptr[0], ptr[1], strlen2 * sizeof(int));
        for (j = 0; j < strlen2; j++) {
            if (s[i] == t[j]) {
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

PyMODINIT_FUNC
PyInit_lcs(void)
{
    return moduleinit();
}
