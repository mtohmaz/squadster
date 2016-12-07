import { Injectable } from '@angular/core';
import { Headers, Http, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Event } from './event';
import { EventListResponse } from './eventListResponse';
import { Comment } from './comment';
import { CommentListResponse } from './commentListResponse';

@Injectable()
export class EventService {

  private apiSessionUrl = '/api/session/';
  private usersUrl = '/api/users/';
  private eventsUrl = 'https://localhost:80/api/events/';
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getCurrentUserId(){
    return this.http.get(this.apiSessionUrl)
        .map(response => response.json());
  }

  joinEvent(event_id: number): Promise<Event[]> {
    return this.http.post(this.eventsUrl + event_id + "/attendees/", {headers:this.headers})
        .toPromise()
        .then(response => response.json() as Event[])
        .catch(this.handleError);
  }

  leaveEvent(event_id: number, user_id: number) {
    return this.http.delete(this.eventsUrl + event_id + "/attendees/" + user_id, {headers:this.headers})
        .map(response => response.json());
  }

  getEvent(event_id: number): Promise<Event> {
    return this.http.get(this.eventsUrl + event_id)
        .toPromise()
        .then(response => response.json() as Event)
        .catch(this.handleError);
  }

  getComments(event_id: number, page: number) {
    return this.http.get(this.eventsUrl + event_id + "/comments/?page=" + page)
        .map(response => <CommentListResponse>response.json());
  }

  getEvents(lat: number, lon: number, radius: number, s: string, page: number) {
    return this.http.get(this.eventsUrl + "?s=" + s +"&radius=" + radius + "&lat=" + lat + "&lon=" + lon +"&page=" + page)
        .map(response => <EventListResponse>response.json());
  }

  getAttendedEvents(userId: number, page: number){
    return this.http.get(this.usersUrl + userId +'/attendedevents/?page=' + page)
        .map(response => <EventListResponse>response.json());
  }

  getHostedEvents(userId: number, page: number){
    return this.http.get(this.usersUrl + userId +'/hostedevents/?page=' + page)
        .map(response => <EventListResponse>response.json());
  }

  addComment(commentUrl: string, comment: string): Promise<string> {
    return this.http.post(commentUrl, JSON.stringify({text: comment}), {headers: this.headers})
        .toPromise()
        .then(response => response.json())
        .catch(this.handleError);
  }

  create(title: string, date: Date, max_attendees: number, description: string, location: string, lat: number, lon: number): Promise<string> {
    return this.http
        .post(this.eventsUrl, JSON.stringify({title: title, date: date, max_attendees: max_attendees, description: description, location: location, lat: lat, lon: lon}), {headers: this.headers})
        .toPromise()
        .then(response => response.json())
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
