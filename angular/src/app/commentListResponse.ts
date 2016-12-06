import { Injectable } from '@angular/core';
import { Comment } from './comment';

export interface CommentListResponse {
  count: number;
  next: string;
  previous: string;
  results: Comment[];
}
