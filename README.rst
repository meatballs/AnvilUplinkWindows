Anvil Uplink Windows
====================

A library to run uplink code for `Anvil <https://anvil.works/>`_ applications as
a Windows Service.

Installation
------------
.. code-block::

    pip install anvil_uplink_windows


Usage
-----

The library contains a class which you can import and subclass to create a
Windows service.

Your subclass will need to include attributes for its name and a method named
'SvcDoRun' This is the code  that will be executed when the service starts. If
you only need to connect to an anvil app, there is a method which you can call
to do that.

Here is an example which loads the anvil key from an environment variable::

    import os
    from anvil_uplink_windows.service import AnvilWindowsService


    class ExampleService(AnvilWindowsService):

        _svc_name_ = 'ExampleService'
        _svc_display_name_ = 'Example Service'

        def SvcDoRun(self):
            anvil_key = os.environ['ANVIL_KEY']
            super().run(anvil_key)


If you need to run additional code beyond simply connecting to anvil, you can
pass callables and arguments to be executed both pre and post connection::


    import os
    from anvil_uplink_windows.service import AnvilWindowsService


    class ExampleService(AnvilWindowsService):

        _svc_name_ = 'ExampleService'
        _svc_display_name_ = 'Example Service'

        def pre_connect(args):
            # do something here
            pass

        def post_connect(args):
            # do something else
            pass

        def SvcDoRun(self):
            anvil_key = os.environ['ANVIL_KEY']
            super().run(
                anvil_key,
                pre_connect=pre_connect,
                pre_connect_args=[1, 2 3],
                post_connect=post_connect,
                post_connect_args=[4, 5, 6])


Anvil callable functions can be included in the same module::

    import os
    import anvil.server
    from anvil_uplink_windows.service import AnvilWindowsService


    @anvil.server.callable
    def hello():
        return 'Hello World!'


    class ExampleService(AnvilWindowsService):

        _svc_name_ = 'ExampleService'
        _svc_display_name_ = 'Example Service'

        def SvcDoRun(self):
            anvil_key = os.environ['ANVIL_KEY']
            super().run(anvil_key)


And, finally, you will need to import and call a function from within the
libary::

    import os
    import anvil.server
    from anvil_uplink_windows.service import AnvilWindowsService, manage_service


    @anvil.server.callable
    def hello():
        return 'Hello World!'


    class ExampleService(AnvilWindowsService):

        _svc_name_ = 'ExampleService'
        _svc_display_name_ = 'Example Service'

        def SvcDoRun(self):
            anvil_key = os.environ['ANVIL_KEY']
            super().run(anvil_key)

    if __name__ == '__main__':
        manage_service(ExampleService, sys.argv)


You can use the excellent `Pyinstaller libary <http://www.pyinstaller.org/>`_ to
package your code as a Windows executable. Here is an pyinstaller spec file for
the example code above::

    # -*- mode: python -*-

    block_cipher = None

    a = Analysis(['<path to example.py>'],
                  pathex=['<path to directory containining example.py>'],
                  binaries=[],
                  datas=[],
                  hiddenimports=['win32timezone'],
                  hookspath=[],
                  runtime_hooks=[],
                  excludes=[],
                  win_no_prefer_redirects=False,
                  win_private_assemblies=False,
                  cipher=block_cipher)
    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name='ExampleService',
              debug=False,
              strip=False,
              upx=True,
              runtime_tmpdir=None,
              console=True )

which can then be used to build the executable file with::

    pyinstaller pyinstaller.spec

The resulting executable (by default in a folder named 'dist') can then used to
install, start, stop and remove the Windows Service::

    dist\ExampleService.exe install
    dist\ExampleService.exe start
    dist\ExamplerService.exe stop
    dist\ExampleService.exe remove

Acknowledgments
---------------

This work owes debt of gratitude to `Guillaume Vincent's gist <https://gist.github.com/guillaumevincent/d8d94a0a44a7ec13def7f96bfb713d3f>`_.
