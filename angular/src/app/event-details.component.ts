import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Event } from './event';
import { EventService } from './event.service';
import { Comment } from './comment';

@Component({
  selector: 'event-details',
  templateUrl: 'html/event-details.component.html',
  providers: [EventService]
})

export class EventDetailsComponent {
  event: Event;
  comments: Comment[];
  inputComment: string;
  event_id: number;

  totalItems:number;
  currentPage:number = 1;
  maxSize:number = 10;

  constructor(
    private router: ActivatedRoute,
    private eventService: EventService,
    private ref: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.getEvent();
    this.getComments();
  }

  getEvent() {
    this.router.queryParams.forEach((params: Params) => {
      this.event_id = +params['id'] || 0;
      this.currentPage = +params['page'] || 1;
      if (this.event_id != 0) {
        this.eventService.getEvent(this.event_id).then(ret => {
          this.event = ret;
          this.ref.detectChanges();
          this.getComments();
        });
      }
    });
  }

  getComments() {
    this.eventService.getComments(this.event_id, this.currentPage).subscribe(response => {
      this.comments = response.results;
      this.totalItems = response.count;
      this.ref.detectChanges();
    });
  }

  onClick(inputComment: string) {
    this.eventService.addComment(this.event.comments, inputComment).then(response => this.getComments());
  }

  pageChanged(event:any):void {
    this.currentPage = event.page;
    this.getComments();
  }
}
