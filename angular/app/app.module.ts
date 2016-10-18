import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { HttpModule } from '@angular/http';
import { SidebarModule } from 'ng2-sidebar';

import { Ng2BootstrapModule } from 'ng2-bootstrap/ng2-bootstrap';
import { AUTH_PROVIDERS } from 'angular2-jwt';

import { AppComponent } from './app.component';
import { CreateEventComponent } from './create-event.component';
import { EventDetailComponent } from './event-details.component';
import { MyEventsComponent } from './my-events.component';
import { MyEventDetailComponent } from './my-event-details.component';
import { ListViewComponent } from './list-view.component';
import { TopNavComponent } from './top-nav.component';
import { SideNavComponent } from './side-nav.component';
import { LoginComponent } from './login.component';

import { EventService } from './event.service';
import { routing } from './app.routing';

@NgModule({
  imports:      [ BrowserModule, FormsModule, Ng2BootstrapModule, routing, HttpModule, SidebarModule],
  declarations: [
    AppComponent,
    CreateEventComponent,
    EventDetailComponent,
    ListViewComponent,
    MyEventsComponent,
    MyEventDetailComponent,
    TopNavComponent,
    SideNavComponent,
    LoginComponent
    ],
  providers: [
    EventService,
    AUTH_PROVIDERS
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
