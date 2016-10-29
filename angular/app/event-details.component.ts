import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Event } from './event';

@Component({
  selector: 'my-event-detail',
  templateUrl: 'app/html/event-details.component.html'
})

export class EventDetailComponent {
  @Input() event: Event;

  constructor( private router: Router) {}

  onClick() {
    this.router.navigate(['app/create-event'], { queryParams: { id: this.event.event_id }});
  }
}
