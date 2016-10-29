import { Component } from '@angular/core';
import * as moment from 'moment';
import { ActivatedRoute, Params } from '@angular/router';

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
  templateUrl: 'app/html/create-event.component.html',
  styleUrls: ['app/styles/master-styles.css'],
  providers: [EventService]
})
export class CreateEventComponent {

  events: Event[];
  public minDate: Date = void 0;

  constructor(
    private eventService: EventService,
    private route: ActivatedRoute )
  {
    (this.minDate = new Date()).setDate(this.minDate.getDate());
  }

  ngOnInit() {
      this.route.queryParams.forEach((params: Params) => {
        let id = +params['id'] || 0;
        if (id != 0) {
          this.eventService.getEvent(id).then(ret => this.create = ret);
        }
      });
  }

  title = "Create Event";
  create: Event = {
    event_id: null,
    host_id: null,
    title: null,
    date: null,
    max_attendees: null,
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
     this.eventService.create(this.create.title, this.create.date, this.create.max_attendees, this.create.description);
       /*.then(event => {
         this.events.push(event);
       });*/
   }
}
