import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Event } from './event';
import { Create } from './create-event.component';
import { EVENTS } from './mock-events';

@Injectable()
export class EventService {

  private eventsUrl = 'http://localhost:80/api/events/';
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getEvents(): Promise<Event[]> {
    return this.http.get(this.eventsUrl)
                    .toPromise()
                    .then(response => response.json() as Event[])
                    .catch(this.handleError);
  }

  create(host_id: number, title: string, date: Date, max_attendees: number): Promise<Event> {
    return this.http
               .post(this.eventsUrl, JSON.stringify({host_id: host_id, title: title, date: date, max_attendees: max_attendees}), {headers: this.headers})
               .toPromise()
               .then(response => response.json().data)
               .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occured', error);
    return Promise.reject(error.message || error);
  }
}
