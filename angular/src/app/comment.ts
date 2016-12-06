export class Comment {
  comment_id: number;
  parent_event: number;
  date_added: string;
  text: string;
  parent_comment: number;
  children: string;
  summary_fields: {
    author_email: string;
  }
}
