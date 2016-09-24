import { Component } from '@angular/core';

export class Event {
  id: number;
  title: string;
  location: string;
  startDate: string;
  startTime: string;
  currentAttendees: number;
  maxAttendees: number;
  description: string;
  host: host;
}

const EVENTS: Event[] = [
  { id:1, title: 'Bowling', location: 'AMC', startDate: '09/25/2016', startTime: '9:00pm', currentAttendess: 3, maxAttendees: 10, description: 'Meeting new people at bowling.'},
  { id:2, title: 'Dinner', location: 'El Toro', startDate: '09/30/2016', startTime: '9:00pm', currentAttendess: 9, maxAttendees: 10, description: 'Meeting new people for dinner.'},
  { id:3, title: 'Movie', location: 'My apartment', startDate: '10/25/2016', startTime: '9:00pm', currentAttendess: 0, maxAttendees: 2, description: 'Netflix and chill.'},
];

@Component({
  selector: 'my-app',
  template: `
    <h1>{{title}}</h1>
    <h2>Events</h2>
    <ul class="events">
      <li *ngFor="let event of events"
        [class.selected]="event === selectedEvent"
        (click)="onSelect(event)">
        <span class="badge">{{event.id}}</span> {{event.title}}
      </li>
    </ul>
    <div *ngIf="selectedEvent">
      <h2>{{selectedEvent.title}} details:</h2>
      <div><label>Name of Event: </label>{{selectedEvent.title}}</div>
      <div><label>Location: </label>{{selectedEvent.location}}</div>
      <div><label>Description: </label>{{selectedEvent.description}}</div>
      <div><label>Date: </label>{{selectedEvent.startDate}}</div>
      <div><label>Time: </label>{{selectedEvent.startTime}}</div>
      <div><label>Attendees so far: </label> {{selectedEvent.currentAttendess}}/{{selectedEvent.maxAttendees}}</div>
    </div>
    <div>
      <br>
      Create new event (TIE THIS IN WITH MAHMOUD'S PAGE)
    </div>
    
  `,
  styles: [`
    .selected {
      background-color: #CFD8DC !important;
      color: white;
    }
    .events {
      margin: 0 0 2em 0;
      list-style-type: none;
      padding: 0;
      width: 15em;
    }
    .events li {
      cursor: pointer;
      position: relative;
      left: 0;
      background-color: #EEE;
      margin: .5em;
      padding: .3em 0;
      height: 1.6em;
      border-radius: 4px;
    }
    .events li.selected:hover {
      background-color: #BBD8DC !important;
      color: white;
    }
    .events li:hover {
      color: #607D8B;
      background-color: #DDD;
      left: .1em;
    }
    .events .text {
      position: relative;
      top: -3px;
    }
    .events .badge {
      display: inline-block;
      font-size: small;
      color: white;
      padding: 0.8em 0.7em 0 0.7em;
      background-color: #607D8B;
      line-height: 1em;
      position: relative;
      left: -1px;
      top: -4px;
      height: 1.8em;
      margin-right: .8em;
      border-radius: 4px 0 0 4px;
    }
  `]
})


export class AppComponent {
  title = 'Events Nearby';
  events = EVENTS;
  selectedEvent: Event;

  onSelect(event: Event): void {
    this.selectedEvent = event;
  }
}
