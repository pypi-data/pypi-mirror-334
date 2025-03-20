#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>

typedef struct {
    PyObject_HEAD
    PyObject **items;
    Py_ssize_t size;
    Py_ssize_t capacity;
} FastList;

// Constructor for FastList
static int FastList_init(FastList *self, PyObject *args, PyObject *kwds) {
    self->size = 0;
    self->capacity = 4;
    self->items = (PyObject **)malloc(self->capacity * sizeof(PyObject *));
    if (!self->items) {
        PyErr_NoMemory();
        return -1;
    }
    return 0;
}

// Destructor for FastList
static void FastList_dealloc(FastList *self) {
    for (Py_ssize_t i = 0; i < self->size; i++) {
        Py_DECREF(self->items[i]);
    }
    free(self->items);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

// Append method
static PyObject* FastList_append(FastList *self, PyObject *arg) {
    if (self->size >= self->capacity) {
        Py_ssize_t new_capacity = (self->capacity * 3) / 2;
        PyObject **new_items = (PyObject **)realloc(self->items, new_capacity * sizeof(PyObject *));
        if (!new_items) {
            PyErr_NoMemory();
            return NULL;
        }
        self->items = new_items;
        self->capacity = new_capacity;
    }
    Py_INCREF(arg);
    self->items[self->size] = arg;
    self->size++;
    Py_RETURN_NONE;
}

// Method definitions for FastList
static PyMethodDef FastList_methods[] = {
    {"fappend", (PyCFunction)FastList_append, METH_O, "Append an item to the list"},
    {NULL, NULL, 0, NULL}
};

// Define FastList type
static PyTypeObject FastListType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "fastpyx.FastList",
    .tp_basicsize = sizeof(FastList),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)FastList_init,
    .tp_dealloc = (destructor)FastList_dealloc,
    .tp_methods = FastList_methods,
};

// Multiply function
static PyObject* multiply_number(PyObject* self, PyObject *const *args, Py_ssize_t nargs) {
    if (nargs != 2) {
        PyErr_SetString(PyExc_TypeError, "multiply_number() takes exactly 2 arguments");
        return NULL;
    }

    PyObject *py_num1 = args[0], *py_num2 = args[1];
    double num1, num2;

    num1 = PyFloat_Check(py_num1) ? PyFloat_AS_DOUBLE(py_num1) : PyLong_AsDouble(py_num1);
    num2 = PyFloat_Check(py_num2) ? PyFloat_AS_DOUBLE(py_num2) : PyLong_AsDouble(py_num2);

    if (PyErr_Occurred()) {
        return NULL;
    }
    return PyFloat_FromDouble(num1 * num2);
}

// Module method definitions
static PyMethodDef FastPyxMethods[] = {
    {"multiply_number", (PyCFunction)multiply_number, METH_FASTCALL, "Multiply two numbers"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef FastPyxModule = {
    PyModuleDef_HEAD_INIT,
    "fastpyx",
    NULL,
    -1,
    FastPyxMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_fastpyx(void) {
    PyObject *m;

    if (PyType_Ready(&FastListType) < 0)
        return NULL;

    m = PyModule_Create(&FastPyxModule);
    if (!m)
        return NULL;

    Py_INCREF(&FastListType);
    if (PyModule_AddObject(m, "FastList", (PyObject *)&FastListType) < 0) {
        Py_DECREF(&FastListType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
