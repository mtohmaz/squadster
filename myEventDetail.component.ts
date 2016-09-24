import { Component, Input } from '@angular/core';
import { Event } from './event';
@Component({
  selector: 'myEventDetail',
  template: `
    <div *ngIf="event">
      <h2>{{event.title}} details!</h2>
      <div><label>id: </label>{{event.id}}</div>
      <div>
        <label>Title: </label>
        <input [(ngModel)]="event.title" placeholder="title"/>
      </div>
    </div>
  `
})
export class MyEventDetailComponent {
  @Input()
  event: Event;
}
