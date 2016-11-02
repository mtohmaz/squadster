import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Event } from './event';
import { EventService } from './event.service';

@Component({
  selector: 'event-details',
  templateUrl: 'app/html/event-details.component.html',
  providers: [EventService]
})

export class EventDetailsComponent {
  @Input() event: Event;

  constructor(
    private router: ActivatedRoute,
    private eventService: EventService
  ) {}

  ngOnInit() {
    this.router.queryParams.forEach((params: Params) => {
      let id = +params['id'] || 0;
      if (id != 0) {
        this.eventService.getEvent(id).then(ret => this.event = ret);
        console.log(this.event);
      }
    });
  }
}
