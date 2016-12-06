import { Injectable } from '@angular/core';
import { Event } from './event';

export interface EventListResponse {
  count: number;
  next: string;
  previous: string;
  results: Event[];
}
