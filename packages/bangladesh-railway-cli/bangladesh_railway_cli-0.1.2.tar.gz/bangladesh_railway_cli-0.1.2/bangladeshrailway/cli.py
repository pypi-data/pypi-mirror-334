#!/usr/bin/python3

from bangladeshrailway import BangladeshRailway

import json
import os
import click

from datetime import datetime
from tabulate import tabulate as tab
from dotenv import load_dotenv

load_dotenv()

@click.group()
def app():            
    pass

@app.command(help='Search trains using route and date')
def search():
    try:
        src = os.getenv('ETICKET_FROM')
        dest = os.getenv('ETICKET_TO')
        date = os.getenv('ETICKET_DATE')

        token = os.getenv('ETICKET_TOKEN')
        br = BangladeshRailway(token)
        
        data, headers = br.search(src=src, dest=dest, date=date)
        click.echo(tab(data, headers=headers))
    except Exception as e:
        click.echo(click.style(str(e), fg='red'))

@app.command(help='Book seats on a train')
def book():
    try:
        src = os.getenv('ETICKET_FROM')
        dest = os.getenv('ETICKET_TO')
        date = os.getenv('ETICKET_DATE')
        train = os.getenv('ETICKET_TRAIN')
        class_ = os.getenv('ETICKET_CLASS')
        seats = os.getenv('ETICKET_SEATS').split(',')
        
        print(seats)
        
        token = os.getenv('ETICKET_TOKEN')
        br = BangladeshRailway(token)
        
        payload = br.book(src=src, dest=dest, date=date, train=train, class_=class_, seats=seats)
        click.echo(f"Please set ETICKET_FINAL_PAYLOAD={json.dumps(payload)} in .env")
    except Exception as e:
        click.echo(click.style(str(e), fg='red'))

@app.command(help='Verify OTP before confirming')
def verify():
    try:
        payload = os.getenv('ETICKET_FINAL_PAYLOAD')
        otp = os.getenv('ETICKET_OTP')
        
        token = os.getenv('ETICKET_TOKEN')
        br = BangladeshRailway(token)
        br.verify(payload=json.loads(payload), otp=otp)
        
    except Exception as e:
        click.echo(click.style(str(e), fg='red'))

@app.command(help='Confirm purchase')
def confirm():
    try:
        src = os.getenv('ETICKET_FROM')
        dest = os.getenv('ETICKET_TO')
        date = os.getenv('ETICKET_DATE')
        train = os.getenv('ETICKET_TRAIN')
        class_ = os.getenv('ETICKET_CLASS')
        seats = os.getenv('ETICKET_SEATS').split(',')
        names = os.getenv('ETICKET_NAMES').split(',')

        payload = os.getenv('ETICKET_FINAL_PAYLOAD')
        otp = os.getenv('ETICKET_OTP')
        email = os.getenv('ETICKET_EMAIL')
        phone = os.getenv('ETICKET_PHONE')
        
        token = os.getenv('ETICKET_TOKEN')
        br = BangladeshRailway(token)
        url = br.confirm(
            src=src,
            dest=dest,
            date=date,
            class_=class_,
            count=len(seats),
            payload=json.loads(payload),
            otp=otp,
            email=email,
            phone=phone,
        )
        
        click.echo(f"Tickets confirmed. Please visit {url} to pay")
        
    except Exception as e:
        click.echo(click.style(str(e), fg='red'))

if __name__ == "__main__":
    app()