codeTable = [ "en", "fr", "en", "sv", "en", "it", "en", "es", "en" ]

import argostranslate.package, argostranslate.translate
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
for i in range(len(codeTable) - 1):
    available_package = list(
        filter(
            lambda x: x.from_code == codeTable[i] and x.to_code == codeTable[i + 1], available_packages
        )
    )[0]
    download_path = available_package.download()
    argostranslate.package.install_from_path(download_path)
    print(codeTable[i] + " to " + codeTable[i + 1] + " package installed", flush = True)