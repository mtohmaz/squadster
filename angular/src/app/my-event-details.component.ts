import { Component, Input } from '@angular/core';
import { Event } from './event';
@Component({
  selector: 'myEventDetail',
  templateUrl: 'html/my-event-details.component.html'
})
export class MyEventDetailComponent {
  @Input()
  event: Event;
}
