// SPDX-License-Identifier: Apache-2.0
// Author: Sekiraw

#include <Python.h>
#ifdef _WIN32
#include <windows.h>
#include <shobjidl.h>
#include <combaseapi.h>

// File/Folder Picker Function
static PyObject* filepicker_open(PyObject *self, PyObject *args, PyObject *kwargs) {
    const char *mode = "file";
    static char *kwlist[] = {"mode", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|s", kwlist, &mode)) {
        return NULL;
    }

    // Initialize COM library
    HRESULT hr = CoInitialize(NULL);
    if (FAILED(hr)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to initialize COM.");
        return NULL;
    }

    // Folder selection mode
    if (strcmp(mode, "folder") == 0) {
        IFileDialog *pfd = NULL;

        // Create the FileOpenDialog object
        hr = CoCreateInstance(&CLSID_FileOpenDialog, NULL, CLSCTX_INPROC_SERVER,
                              &IID_IFileDialog, (void **)&pfd);
        if (FAILED(hr)) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to create FileOpenDialog.");
            CoUninitialize();
            return NULL;
        }

        // Configure dialog options to pick folders
        DWORD options = 0;
        pfd->lpVtbl->GetOptions(pfd, &options);
        pfd->lpVtbl->SetOptions(pfd, options | FOS_PICKFOLDERS);

        // Show dialog and get result
        hr = pfd->lpVtbl->Show(pfd, NULL);
        if (SUCCEEDED(hr)) {
            IShellItem *psi = NULL;
            hr = pfd->lpVtbl->GetResult(pfd, &psi);
            if (SUCCEEDED(hr)) {
                PWSTR folderPath = NULL;
                hr = psi->lpVtbl->GetDisplayName(psi, SIGDN_FILESYSPATH, &folderPath);
                if (SUCCEEDED(hr)) {
                    char result[MAX_PATH] = {0};
                    wcstombs(result, folderPath, MAX_PATH);
                    CoTaskMemFree(folderPath);
                    psi->lpVtbl->Release(psi);
                    pfd->lpVtbl->Release(pfd);
                    CoUninitialize();
                    return PyUnicode_FromString(result);
                }
                psi->lpVtbl->Release(psi);
            }
        }

        pfd->lpVtbl->Release(pfd);
        CoUninitialize();
        Py_RETURN_NONE;
    }

    // Default file picker mode
    char filename[MAX_PATH] = {0};
    OPENFILENAME ofn = {0};

    ofn.lStructSize = sizeof(ofn);
    ofn.lpstrFile = filename;
    ofn.nMaxFile = sizeof(filename);
    ofn.lpstrFilter = "All Files\0*.*\0";
    ofn.Flags = OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST;

    if (GetOpenFileName(&ofn)) {
        CoUninitialize();
        return PyUnicode_FromString(filename);
    }

    CoUninitialize();
    Py_RETURN_NONE;
}

#endif

// Python Module Setup
static PyMethodDef FPickerMethods[] = {
    {"open", (PyCFunction)filepicker_open, METH_VARARGS | METH_KEYWORDS, "Open a file or folder picker dialog"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fpickermodule = {
    PyModuleDef_HEAD_INIT,
    "fpicker",
    NULL,
    -1,
    FPickerMethods
};

PyMODINIT_FUNC PyInit_fpicker(void) {
    return PyModule_Create(&fpickermodule);
}