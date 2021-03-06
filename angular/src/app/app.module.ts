import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule } from '@angular/http';

import { Ng2BootstrapModule } from 'ng2-bootstrap/ng2-bootstrap';
import { AgmCoreModule } from 'angular2-google-maps/core';
import { SimpleNotificationsModule } from 'angular2-notifications';

import { AppComponent } from './app.component';
import { CreateEventComponent } from './create-event.component';
import { EventDetailsComponent } from './event-details.component';
import { MyEventsComponent } from './my-events.component';
import { MyEventDetailComponent } from './my-event-details.component';
import { ListViewComponent } from './list-view.component';
import { TopNavComponent } from './top-nav.component';
import { SearchBarComponent } from './search-bar.component';
import { LoginComponent } from './login.component';
import { MapComponent } from './map.component';
import { FiltersComponent } from './filters.component';

import { EventService } from './event.service';
import { routing } from './app.routing';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    Ng2BootstrapModule,
    SimpleNotificationsModule,
    routing,
    HttpModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCQB9nQSw16-SkmsJQS-Jk7mskFKhU2U0Y',
      libraries: ['places']
    })
  ],
  declarations: [
    AppComponent,
    CreateEventComponent,
    EventDetailsComponent,
    ListViewComponent,
    MyEventsComponent,
    MyEventDetailComponent,
    TopNavComponent,
    SearchBarComponent,
    LoginComponent,
    MapComponent,
    FiltersComponent
  ],
  providers: [
    EventService,
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
