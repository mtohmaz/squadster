import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Event } from './event';

@Injectable()
export class EventService {

  private eventsUrl = 'http://localhost:80/api/events/';
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getAllEvents(): Promise<Event[]> {
    return this.http.get(this.eventsUrl)
                    .toPromise()
                    .then(response => response.json() as Event[])
                    .catch(this.handleError);
  }

  getEvent(event_id: number): Promise<Event> {
    return this.http.get(this.eventsUrl + event_id)
                    .toPromise()
                    .then(response => response.json() as Event)
                    .catch(this.handleError);
  }

  create(title: string, date: Date, max_attendees: number, description: string): Promise<string> {
    return this.http
               .post(this.eventsUrl, JSON.stringify({title: title, date: date, max_attendees: max_attendees, description: description}), {headers: this.headers})
               .toPromise()
               .then(response => console.log(response.json()))
               .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    if (error.status == 400)
      return Promise.resolve("Bad Request");
    else if (error.status == 401)
      return Promise.resolve("Not logged in");
    else if (error.status == 403)
      return Promise.resolve("Not authenticated");
    else
      return Promise.reject(error.message || error);
  }
}
