import { Component } from '@angular/core';
import * as moment from 'moment';

import { Event } from './event';
import { EventService } from './event.service';

export class Create {
  title: string;
  location: string;
  eventDate: Date;
  eventTime: Date;
  maxAttendees: number;
  description: string;
}

@Component({ //tells angular that this file is a component.
  selector: 'create-event',
  template: `
  <h2>{{ title }}</h2>
  <div class="body">
    <label>Event Title: </label>
    <input [(ngModel)]="create.title">
    <br><br>

    <label>Event Location: </label>
    <input [(ngModel)]="create.location">
    <br><br>

    <label>Date: </label>
    <datepicker [(ngModel)]="create.eventDate" [showWeeks]="false" [minDate]="minDate"></datepicker>

    <label>&nbsp;Time: </label>
    <input type="time" [(ngModel)]="create.eventTime">
    <br><br>

    <label>Max Attendees: </label>
    <input [(ngModel)]="create.maxAttendees">
    <br><br>

    <label>Description: </label>
    <input [(ngModel)]="create.description">
    <br><br>

    <button (click)="add(create)">Add</button>
  </div>
  `,
  styleUrls: ['app/styles/master-styles.css'],
  providers: [EventService]
})
export class CreateEventComponent {

  events: Event[];
  public minDate: Date = void 0;

  constructor( private eventService: EventService ){
    (this.minDate = new Date()).setDate(this.minDate.getDate() - 1000);
  }

  title = "Create Event";
  create: Create = {
    title: null,
    location: null,
    eventDate: null,
    eventTime: null,
    maxAttendees: null,
    description: null
  };

  /*ngOnInit(): void {
    this.route.params.forEach((params: Params) => {
       let id = +params['id'];
       this.eventService.getEvents(id)
         .then(hero => this.event = event);
       });
    }*/

   add(event: Create): void {
     if (!event) { return; }
     this.eventService.create(1, this.create.title, this.create.eventDate, this.create.maxAttendees);
       /*.then(event => {
         this.events.push(event);
       });*/
   }
}
