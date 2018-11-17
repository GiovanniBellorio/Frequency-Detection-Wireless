'''
Created on 26 0tt 2018

Controller dell'applicazione web

@author: Giovanni, Davide
'''

import os
import logging
from django.utils.html import strip_tags
from flask import Flask, session, request, flash, escape, redirect, url_for
from flask_sessionstore import Session
from flask.templating import render_template
from Model import Model


sessione = Session()
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__) # Applicazione Flask!
app.model = Model()


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route('/')
def home():
    return render_template('login.html')
 
@app.route('/login', methods=['POST'])
def login():
    username = strip_tags(request.form['username'])
    password = strip_tags(request.form['pass'])
    password_codificata = app.model.make_md5(app.model.make_md5(password))
    num_rows, id_utente = app.model.getCountUsernamePassword(username, password_codificata)
    if num_rows == 1:
        session['logged_in'] = True
        session['username']  = username
        session['id_utente'] = id_utente
        return redirect(url_for('registro'))
    else:
        flash('wrong password!')
        return redirect(url_for('home'))
 
@app.route("/logout", methods=['POST'])
def logout():    
    session['logged_in'] = False
    session['username']  = ""
    session['id_utente'] = 0
    return redirect(url_for('home'))

@app.route("/view_modify_pwd", methods=['POST'])
def view_modify_pwd():
    if session.get('logged_in'):
        return render_template('modify_pwd.html')
    else:
        flash('wrong password!')
        return redirect(url_for('home'))

@app.route("/modify_pwd", methods=['POST'])
def modify_pwd():
    if session.get('logged_in'):
        password1 = strip_tags(request.form['pass1'])
        password2 = strip_tags(request.form['pass2'])
        if password1 == password2:
            password_codificata = app.model.make_md5(app.model.make_md5(password2))
            id_utente = session.get('id_utente')
            ack_pwd = app.model.updateUserPwd(id_utente, password_codificata)
            if ack_pwd:
                return redirect(url_for('registro'))
            else:
                return redirect(url_for('view_modify_pwd'))
        else:
            return view_modify_pwd()
    else:
        flash('wrong password!')
        return redirect(url_for('home'))
        

@app.route("/registro")
def registro():
    if session.get('logged_in'):
        username  = session.get('username')
        id_utente = session.get('id_utente')
        matricola = app.model.getMatricola(id_utente)
        ruolo = app.model.getRuoloUsername(id_utente)
        # 0 --> admin, 
        # 1 --> supervisore, 
        # 2 --> utente normale
        if ruolo == 2:
            frequenza = app.model.getFrequenzaUsername(id_utente)
            return render_template('registro.html', username=username, matricola=matricola, id_utente=id_utente, ruolo=ruolo, frequenza=frequenza)
        #elif ruolo == 1:
        elif ruolo == 0:
            utenti_punteggi = app.model.getUtentiPunteggi()
            supervisori_punteggi = app.model.getSupervisoriPunteggi()
            return render_template('registro.html', username=username, ruolo=ruolo, supervisori_punteggi=supervisori_punteggi, utenti_punteggi=utenti_punteggi)
        else:
            flash('wrong password!')
            return redirect(url_for('home'))
    else:
        flash('wrong password!')
        return redirect(url_for('home'))
    
@app.route("/registro_supervisori", methods=['POST'])
def registro_supervisori():
    if session.get('logged_in'):
        username  = session.get('username')
        id_utente = session.get('id_utente')
        ruolo = app.model.getRuoloUsername(id_utente)
        supervisori_punteggi = app.model.getSupervisoriPunteggi()
        return render_template('registro.html', username=username, ruolo=ruolo, supervisori_punteggi=supervisori_punteggi)
    else:
        flash('wrong password!')
        return redirect(url_for('home'))
    
@app.route("/registro_utenti", methods=['POST'])
def registro_utenti():
    if session.get('logged_in'):
        username  = session.get('username')
        id_utente = session.get('id_utente')
        ruolo = app.model.getRuoloUsername(id_utente)
        utenti_punteggi = app.model.getUtentiPunteggi()
        return render_template('registro.html', username=username, ruolo=ruolo, utenti_punteggi=utenti_punteggi)
    else:
        flash('wrong password!')
        return redirect(url_for('home'))
    
@app.route("/profilo", methods=['POST'])
def profilo():
    if session.get('logged_in'):
        username  = session.get('username')
        id_utente = session.get('id_utente')
        matricola = request.form['matricola']
        id, utente = app.model.getProfiloUtente(matricola)
        ruolo = app.model.getRuoloUsername(id)
        session['ruolo'] = ruolo
        if ruolo == 0:
            ruolo = "admin"
        elif ruolo == 1:
            ruolo = "supervisore"
        elif ruolo == 2:
            ruolo = "utente"
        frequenza = app.model.getFrequenzaUsername(id)
        return render_template('profilo.html', username=username, id_utente=id_utente, utente=utente, frequenza=frequenza, ruolo=ruolo)
    else:
        flash('wrong password!')
        return redirect(url_for('home'))
    
@app.route("/cambio_ruolo", methods=['POST'])
def cambio_ruolo():
    ruolo        = session.get('ruolo')
    option_ruolo = request.form['option_ruolo']
    if ruolo == 1 and option_ruolo == "Supervisore":
        pass
    elif ruolo == 2 and option_ruolo == "Utente":
        pass
    else:
        # CAMBIO RUOLO DA IMPLEMENTARE
        print("diversi")
    
    session['ruolo'] = ""
    return redirect(url_for('registro'))

if __name__ == '__main__': # Questo if deve essere ultima istruzione.
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_KEY']   = os.urandom(16)
    app.secret_key = os.urandom(12)
    sessione.init_app(app)
    app.run(debug=True, use_reloader=True)  # Debug permette anche di ricaricare i file modificati senza rinizializzare il web server.
