import { Component } from '@angular/core';
import {Event } from './event';
const EVENTS: Event[] = [
  { id: 11, title: 'Mr. Nice' },
  { id: 12, title: 'Narco' },
  { id: 13, title: 'Bombasto' },
  { id: 14, title: 'Celeritas' },
  { id: 15, title: 'Magneta' },
  { id: 16, title: 'RubberMan' },
  { id: 17, title: 'Dynama' },
  { id: 18, title: 'Dr IQ' },
  { id: 19, title: 'Magma' },
  { id: 20, title: 'Tornado' }
];
@Component({
  selector: 'my-app',
  template: `
    <h1>{{title}}</h1>
    <h2>My Events</h2>
    <ul class="events">
      <li *ngFor="let event of events"
        [class.selected]="event === selectedEvent"
        (click)="onSelect(event)">
        <span class="badge">{{event.id}}</span> {{event.title}}
      </li>
    </ul>
    <myEventDetail [event]="selectedEvent"></myEventDetail>
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
  title = 'My Event List';
  events = EVENTS;
  selectedEvent: Event;
  onSelect(event: Event): void {
    this.selectedEvent = event;
  }
}
