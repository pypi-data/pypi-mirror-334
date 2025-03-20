import click
from .bpdb import BPDBSmartMeterAPI
from tabulate import tabulate

@click.group()
def app():
    pass

@click.command()
@click.argument('phone_number')
def send_otp(phone_number):
    apiclient = BPDBSmartMeterAPI()
    apiclient.send_otp(phone_number=phone_number)
    click.echo(f"OTP sent to {phone_number}")

@click.command()
@click.argument('phone_number')
@click.argument('otp')
def login(phone_number, otp):
    apiclient = BPDBSmartMeterAPI()
    apiclient.login(phone_number=phone_number, otp=otp)
    click.echo(f"Logged in with phone number {phone_number}")

@click.command()
@click.argument('customer_number')
@click.argument('meter_number')
def recharge_info(customer_number, meter_number):
    apiclient = BPDBSmartMeterAPI()
    data = apiclient.recharge_info(customer_number=customer_number, meter_number=meter_number)
    table = [
        [entry['date'], entry['gross_amount'], entry['energy_cost'], entry['tokens']]
        for entry in data
    ]
    click.echo(tabulate(table, headers=['Date', 'Gross Amount', 'Energy Cost', 'Tokens'], tablefmt='pretty'))

@click.command()
def consumer_info():
    apiclient = BPDBSmartMeterAPI()
    data = apiclient.consumer_info()
    table = [
        ['Division', data['division']],
        ['Meter Type', data['meterType']],
        ['Account Type', data['accountType']],
        ['S&D Division', data['sndDivision']],
        ['Sanction Load', data['sanctionLoad']],
        ['Customer Name', data['customerName']],
        ['Customer Address', data['customerAddress']],
        ['Tariff Category', data['tariffCategory']]
    ]
    click.echo(tabulate(table, tablefmt='pretty'))

app.add_command(send_otp)
app.add_command(login)
app.add_command(recharge_info)
app.add_command(consumer_info)

if __name__ == '__main__':
    app()