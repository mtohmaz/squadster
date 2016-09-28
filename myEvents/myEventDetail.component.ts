import { Component, Input } from '@angular/core';
import { Event } from './event';
@Component({
  selector: 'myEventDetail',
  template: `
    <div *ngIf="event">
      <h2>{{event.title}} details!</h2>
		<div><label>Event ID: </label> {{event.id}} </div>
		<div><label>Title: </label>{{event.title}}</div>
        <div><label>Host name: </label>{{event.host}}</div>
        <div><label>Title: </label> {{event.date}}</div>
        <div><label>Max Guests: </label> {{event.maxGuests}}</div>
        <div><label>Location Name: </label> {{event.locationName}}</div>
        <div><label>Location Address: </label> {{event.locationAddress}}</div>
        <div><label>Tag Name: </label> {{event.tagName}}</div>
        <div><label>Description: </label> {{event.description}}</div>
    </div>
  `
})
export class MyEventDetailComponent {
  @Input()
  event: Event;
}
