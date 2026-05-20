import requests

URL = "https://ideadif.adif.es/gservices/Tramificacion/wfs?request=GetFeature"

def main():
    output_formats = ["text/csv", "json", "kml"]
    for output_format in output_formats:
        get_file_as(output_format)

def get_file_as(output):
    params = "&service=WFS&version=2.0.0&typename=Tramificacion:Dependencias&outputFormat=" + output

    try:
        r = requests.get(URL, params=params, timeout=15)
        output_filename = "files/DependenciasAdif" + get_extension(output)
        with open(output_filename, "w", encoding="utf8") as file:
            print("Generating " + output_filename)
            for lines in r.text:
                file.write(lines)
    except requests.exceptions.Timeout:
        print("Timeout :( ")

def get_extension(output):
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
