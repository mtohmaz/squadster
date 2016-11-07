import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Event } from './event';
import { EventService } from './event.service';

@Component({
  selector: 'event-details',
  templateUrl: 'html/event-details.component.html',
  providers: [EventService]
})

export class EventDetailsComponent {
  event: Event;
  comments: string[];
  inputComment: string;

  constructor(
    private router: ActivatedRoute,
    private eventService: EventService
  ) {}

  ngOnInit() {
    this.getComments();
  }

  getComments() {
    this.router.queryParams.forEach((params: Params) => {
      let id = +params['id'] || 0;
      if (id != 0) {
        this.eventService.getEvent(id).then(ret => this.event = ret);
        this.eventService.getComments(id).then(com => this.comments = com.slice().reverse());
      }
    });
  }

  onClick(inputComment: string) {
    this.eventService.addComment(this.event.comments, inputComment);
    this.getComments();
  }
}
