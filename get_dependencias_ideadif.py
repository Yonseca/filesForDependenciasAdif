

import json
import requests

URL = "https://ideadif.adif.es/gservices/Tramificacion/wfs?request=GetFeature"


def main():
    """ Start here: set output files and get info from endpoint """
    output_formats = ["text/csv", "json", "kml"]
    for output_format in output_formats:
        get_file_as(output_format)

def get_file_as(output):
    """
        For a given output filetype,
        set the needed params for URL,
        request the data from URL,
        get all the data,
        format the data if it's JSON,
        then write data to a file.

        :argument output: OutputFormat value accepted by the endpoint.
    """

    # Params needed to complete the request URL
    params = "&service=WFS&version=2.0.0&typename=Tramificacion:Dependencias&outputFormat=" + output

    try:
        r = requests.get(URL, params=params, timeout=15)
        output_filename = "files/DependenciasAdif" + get_extension(output)
        with open(output_filename, "w", encoding="utf8") as file:
            print("Generating " + output_filename)
            if output == "json": # Make it beautiful, as it's gonna be too big
                parsed_json = json.loads(r.text)
                file.write(json.dumps(parsed_json, indent=4, ensure_ascii=False))
            else:
                for lines in r.text:
                    file.write(lines)
    except requests.exceptions.Timeout:
        print("Timeout :( ")

def get_extension(output):
    """
        Given an output filetype, return its file extension

        :argument output: outputFormat value accepted by the endpoint. If wrong of not implemented,
            an empty string is returned and the resulting file, if any, will have no extension.

        :returns str with a file extension for a given output
    """

    match output:
        case "text/csv":
            return ".csv"
        case "json":
            return ".json"
        case "kml":
            return ".kml"
        case _:
            return ""

if __name__ == "__main__":
    main()
