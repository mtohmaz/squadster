import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';

import { Ng2BootstrapModule } from 'ng2-bootstrap/ng2-bootstrap';
import { AppComponent } from './app.component';
import { CreateEventComponent } from './create-event.component';
import { EventDetailComponent } from './event-details.component';
import { MyEventsComponent } from './my-events.component';
import { MyEventDetailComponent } from './my-event-details.component';
import { ListViewComponent } from './list-view.component';
import { routing } from './app.routing';

@NgModule({
  imports:      [ BrowserModule, FormsModule, Ng2BootstrapModule, routing ],
  declarations: [
    AppComponent,
    CreateEventComponent,
    EventDetailComponent,
    ListViewComponent,
    MyEventsComponent,
    MyEventDetailComponent
    ],
  bootstrap: [
    AppComponent,
    CreateEventComponent,
    EventDetailComponent,
    ListViewComponent,
    MyEventsComponent,
    MyEventDetailComponent
  ]
})
export class AppModule { }
