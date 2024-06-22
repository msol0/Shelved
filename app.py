from flask import Flask, request, make_response, jsonify, render_template, redirect, url_for
from pony import orm
from itertools import groupby

DB = orm.Database()

app = Flask(__name__)


class Knjiga(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naslov = orm.Required(str)
    autor = orm.Required(str)
    zanr = orm.Required(str)
    izdavac = orm.Required(str)
    godina_izdanja = orm.Required(int)
    broj_stranica = orm.Required(int)


DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)

# dodaj_knjigu

def post_knjigu(json_request):
    try:
        data = json_request

        with orm.db_session:
            Knjiga(naslov=data['naslov'], autor=data['autor'], zanr=data['zanr'], izdavac=data['izdavac'],
                   godina_izdanja=data['godina_izdanja'], broj_stranica=data['broj_stranica'])
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


@app.route("/dodaj/knjigu", methods=["POST", "GET"])
def dodaj_knjigu():
    if request.method == "POST":
        try:
            json_request = {}
            for key, value in request.form.items():
                if value == "":
                    json_request[key] = None
                else:
                    json_request[key] = value
        except Exception as e:
            response = {"response": str(e)}
            return make_response(jsonify(response), 400)

        response = post_knjigu(json_request)

        if response["response"] == "Success":
            return make_response(render_template("addKnjiga.html"), 200)
        return make_response(jsonify(response), 400)
    else:
        return make_response(render_template("addKnjiga.html"), 200)


# dohvati_knjigu
def get_knjige():
    try:
        with orm.db_session:
            db_query = orm.select(x for x in Knjiga)[:]
            results_list = []
            for r in db_query:
                results_list.append(r.to_dict())
            response = {"response": "Success", "data": results_list}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


def get_knjige_by_id(knjiga_id):
    try:
        with orm.db_session:
            result = Knjiga[knjiga_id].to_dict()
            response = {"response": "Success", "data": result}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


@app.route("/knjiga/<int:knjiga_id>", methods=["GET"])
def dohvati_knjigu(knjiga_id):
    response = get_knjige_by_id(knjiga_id)
    if response["response"] == "Success":
        return make_response(jsonify(response["data"]), 200)
    return make_response(jsonify(response), 400)


@app.route("/vrati/knjige", methods=["GET"])
def vrati_knjige():
    if request.args and 'id' in request.args:
        knjiga_id = int(request.args.get("id"))
        response = get_knjige_by_id(knjiga_id)
        if response["response"] == "Success":
            return make_response(render_template("popis.html", show_search=True, data=response["data"]), 200)
        return make_response(jsonify(response), 400)

    response = get_knjige()
    if response["response"] == "Success":
        return make_response(render_template("popis.html", show_search=True, knjige=response["data"]), 200)
    return make_response(jsonify(response), 400)


@app.route("/lista/<int:knjiga_id>", methods=["GET"])
def dohvati_odabranu_knjigu(knjiga_id):
    response = get_knjige_by_id(knjiga_id)
    if response["response"] == "Success":
        return make_response(jsonify(response["data"]), 200)
    return make_response(jsonify(response), 400)


# uredi_knjigu

def patch_knjigu(knjiga_id, json_request):
    try:
        with orm.db_session:
            to_update = Knjiga[knjiga_id]
            if 'naslov' in json_request:
                to_update.naslov = json_request['naslov']
            if 'autor' in json_request:
                to_update.autor = json_request['autor']
            if 'zanr' in json_request:
                to_update.zanr = json_request['zanr']
            if 'izdavac' in json_request:
                to_update.izdavac = json_request['izdavac']
            if 'godina_izdanja' in json_request:
                to_update.godina_izdanja = json_request['godina_izdanja']
            if 'broj_stranica' in json_request:
                to_update.broj_stranica = json_request['broj_stranica']

            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


@app.route("/knjiga/<int:knjiga_id>", methods=["PATCH"])
def uredi_knjigu(knjiga_id):
    try:
        json_request = request.json
    except Exception as e:
        response = {"response": str(e)}
        return make_response(jsonify(response), 400)

    response = patch_knjigu(knjiga_id, json_request)
    if response["response"] == "Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


# obrisi_knjigu

def delete_knjigu(knjiga_id):
    try:
        with orm.db_session:
            to_delete = Knjiga[knjiga_id]
            to_delete.delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


@app.route("/knjiga/<int:knjiga_id>", methods=["DELETE"])
def obrisi_obavezu(knjiga_id):
    response = delete_knjigu(knjiga_id)
    if response["response"] == "Success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


# sortiraj

@app.route('/sorting')
@orm.db_session()
def sorting():
    sort_knjige = request.args.get('sort_knjige', 'id')

    knjige_query = Knjiga.select()
    if sort_knjige == 'naslov':
        knjige_query = knjige_query.order_by(Knjiga.naslov)
    elif sort_knjige == 'autor':
        knjige_query = knjige_query.order_by(Knjiga.autor)
    elif sort_knjige == 'zanr':
        knjige_query = knjige_query.order_by(Knjiga.zanr)
    elif sort_knjige == 'izdavac':
        knjige_query = knjige_query.order_by(Knjiga.izdavac)
    elif sort_knjige == 'godina_izdanja':
        knjige_query = knjige_query.order_by(Knjiga.godina_izdanja)
    else:
        knjige_query = knjige_query.order_by(Knjiga.broj_stranica)

    knjige = knjige_query[:]

    return make_response(render_template('popis.html', knjige=knjige, sort_knjige=sort_knjige, show_search=True), 200)


# filter po žanru

@app.route('/filter_by_genre', methods=["GET"])
@orm.db_session()
def filter_by_genre():
    zanr = request.args.get('zanr')
    knjige_query = Knjiga.select()

    if zanr:
        with orm.db_session:
            knjige = orm.select(knjiga for knjiga in knjige_query if knjiga.zanr == zanr)[:]
    else:
        with orm.db_session:
            knjige = orm.select(knjiga for knjiga in knjige_query)[:]
    return make_response(render_template('popis.html', knjige=knjige, show_search=True), 200)


# pretraži

@app.route("/search", methods=["GET"])
@orm.db_session()
def pretrazi():
    term = request.args.get('search_term')
    knjige_query = Knjiga.select()
    knjige = [knjiga for knjiga in knjige_query if
              term.lower() in [word.lower() for value in knjiga.to_dict().values() for word in str(value).split()]]
    return make_response(render_template("popis.html", knjige=knjige, show_search=True), 200)


# vizualizacija po žanru

@orm.db_session
def get_knjige_by_genre():
    try:
        knjige = orm.select(knjiga for knjiga in Knjiga).order_by(Knjiga.zanr)

        grouped_by_genre = groupby(knjige, lambda knjiga: knjiga.zanr)

        result = [{"zanrovi": zanr, "broj_knjiga": len(list(knjige))} for zanr, knjige in grouped_by_genre]

        response = {"response": "Success", "data": {"zanrovi": result}}

        return response

    except Exception as e:
        error_response = {"response": "Error", "error_message": str(e)}
        return error_response

@app.route("/vrati/knjige/zanrovi", methods=["GET"])
def knjige_po_zanrovima():
    try:
        pie_chart_zanrovi = get_knjige_by_genre()

        zanrovi = list(pie_chart_zanrovi.get("data", {}).values())
        return render_template("vizualizacija_zanrovi.html", zanrovi=zanrovi)

    except Exception as e:
        error_response = {"response": "Error", "error_message": str(e)}
        return make_response(jsonify(error_response), 500)




@app.route("/", methods=["GET"])
def home():
    return redirect(url_for('vrati_knjige'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
