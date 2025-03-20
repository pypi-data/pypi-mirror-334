#!/usr/bin/python3

import requests

ETICKET_API = 'https://railspaapi.shohoz.com/v1.0/web'
ETICKET_API_SEARCH = ETICKET_API + '/search-route?from_city={src}&to_city={dest}'
ETICKET_API_BOOKINGS = ETICKET_API + '/bookings/search-trips-v2?from_city={src}&to_city={dest}&date_of_journey={date}&seat_class={class_}'
ETICKET_API_SEATS = ETICKET_API + '/bookings/seat-layout?trip_id={trip_id}&trip_route_id={trip_route_id}'
ETICKET_API_RESERVE = ETICKET_API + '/bookings/reserve-seat'
ETICKET_API_PASSENGER_DETAILS = ETICKET_API + '/bookings/passenger-details'
ETICKET_API_VERIFY_OTP = ETICKET_API + '/bookings/verify-otp'
ETICKET_API_CONFIRM = 'https://railspaapi.shohoz.com/v1.0/web/bookings/confirm'

class BangladeshRailway:
    def __init__(self, token):
        self.headers = {'Authorization': f'Bearer {token}'}

    def _make_request(self, method, url, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        response = requests.request(method, url, **kwargs)
        if response.status_code != 200:
            raise Exception(response.text)
        if 'error' in response.json():
            raise Exception(response.text)
        return response.json()

    def search(self, src, dest, date):
        # response = self._make_request('GET', ETICKET_API_SEARCH.format(src=src, dest=dest))
        response = self._make_request('GET', ETICKET_API_BOOKINGS.format(src=src, dest=dest, date=date, class_='DUMMY'))
        
        data = []
        
        for train in response['data']['trains']:
            seats = []
            
            for seat_types in train['seat_types']:
                seat_counts = seat_types['seat_counts']
                seats.append(f"{seat_types['type']} ({seat_counts['online']})")
            
            data.append([
                train['trip_number'],
                train['departure_date_time'],
                train['travel_time'],
                '\n'.join(seats)
            ])
            
        headers = ['Train Name', 'Departure Time', 'Duration', 'Seat Type', 'Seats']
        return data, headers

    def book(self, src, dest, date, train, class_, seats):
        response = self._make_request('GET', ETICKET_API_BOOKINGS.format(src=src, dest=dest, date=date, class_=class_))
        
        trip_id = None
        trip_route_id = None
        
        for _train in response['data']['trains']:
            if train in _train['trip_number']:
                for seat_types in _train['seat_types']:
                    if seat_types['type'] == class_:
                        trip_id = seat_types['trip_id']
                        trip_route_id = seat_types['trip_route_id']
                        break
        
        if trip_id == None or trip_route_id == None:
            raise Exception('Train/Seat not found')
        
        response = self._make_request('GET', ETICKET_API_SEATS.format(trip_id=trip_id, trip_route_id=trip_route_id))
        
        ticket_ids = []
        
        for coach in response['data']['seatLayout']:
            for layout in coach['layout']:
                for seat in layout:
                    if seat['seat_number'] in seats:
                        ticket_ids.append(seat['ticket_id'])
                        print("Found seat", seat['seat_number'], "with ticket_id", seat['ticket_id'])
                        
        for ticket_id in ticket_ids:
            payload = {
                "route_id": trip_route_id,
                "ticket_id": ticket_id,
            }            
            response = self._make_request('PATCH', ETICKET_API_RESERVE, json=payload)
            print("Booked seat with ticket_id", ticket_id)

        payload = {
            "trip_id": trip_id,
            "trip_route_id": trip_route_id,
            "ticket_ids": ticket_ids,
        }
        
        response = self._make_request('POST', ETICKET_API_PASSENGER_DETAILS, json=payload)
        print("OTP sent to your phone")
        return payload
        
    def verify(self, payload, otp):
        payload = {
            **payload,
            "otp": otp,
        }
                
        response = self._make_request('POST', ETICKET_API_VERIFY_OTP, json=payload)
        
        print(response)
        print("Tickets confirmed")

    def confirm(self, src, dest, date, class_, payload, count, otp, email, phone):
        payload = {
            "is_bkash_online": False,
            "boarding_point_id": 107686153,
            "contactperson": 0,
            "from_city": src,
            "to_city": dest,
            "date_of_journey": date,
            "seat_class": class_,
            "gender": ["male"] * count,
            "page": [
                "",
                ""
            ],
            "passengerType": ["Adult"] * count,
            "pemail": email,
            "pmobile": phone,
            "pname": [
                "FARHANA HOQUE",
                "MD MOZAMMEL HAQUE"
            ],
            # "ppassport": [
            #     "",
            #     ""
            # ],
            # "priyojon_order_id": "null",
            # "referral_mobile_number": "null",
            **payload,
            "isShohoz": 0,
            "enable_sms_alert": 0,
            # "first_name": [
            #     null,
            #     null
            # ],
            # "middle_name": [
            #     null,
            #     null
            # ],
            # "last_name": [
            #     null,
            #     null
            # ],
            # "date_of_birth": [
            #     null,
            #     null
            # ],
            # "nationality": [
            #     null,
            #     null
            # ],
            # "passport_type": [
            #     null,
            #     null
            # ],
            # "passport_no": [
            #     null,
            #     null
            # ],
            # "passport_expiry_date": [
            #     null,
            #     null
            # ],
            # "visa_type": [
            #     null,
            #     null
            # ],
            # "visa_no": [
            #     null,
            #     null
            # ],
            # "visa_issue_place": [
            #     null,
            #     null
            # ],
            # "visa_issue_date": [
            #     null,
            #     null
            # ],
            # "visa_expire_date": [
            #     null,
            #     null
            # ],
            "otp": otp,
            "pg": "visa"
        }
        
        response = self._make_request('PATCH', ETICKET_API_CONFIRM, json=payload)
        
        if 'data' in response:
            return response['data']['redirectUrl']
        else:
            raise Exception(response)
