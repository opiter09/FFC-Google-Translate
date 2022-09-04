codeTable = [ "en", "fr", "en", "sv", "en", "it", "en", "es", "en" ]
import argostranslate.package, argostranslate.translate

def doIt(inputFile, outputFile):
    inFile = open(inputFile, "rb")
    inText = inFile.read().decode("UTF-8", errors = "backslashreplace")
    outFile = open(outputFile, "wb")
    outText = inText

    for i in range(len(codeTable) - 1):
        from_code = codeTable[i]
        to_code = codeTable[i + 1]

        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = list(filter(
            lambda x: x.code == from_code,
            installed_languages))[0]
        to_lang = list(filter(
            lambda x: x.code == to_code,
            installed_languages))[0]
        translation = from_lang.get_translation(to_lang)
        translatedText = translation.translate(outText)
        outText = translatedText
    
    outFile.write(outText.encode("UTF-8", errors = "backslashreplace"))
    inFile.close()
    outFile.close()
    