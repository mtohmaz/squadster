import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ListViewComponent }   from './list-view.component';
import { CreateEventComponent } from './create-event.component';
import { MyEventsComponent } from './my-events.component';
import { LoginComponent } from './login.component';
import { MapComponent } from "./map.component";

const appRoutes: Routes = [
  {
    path: '',
    redirectTo: 'app/list-view',
    pathMatch: 'full'
  },
  {
    path: 'app/login',
    component: LoginComponent
  },
  {
    path: 'app/list-view',
    component: ListViewComponent
  },
  {
    path: 'app/create-event',
    component: CreateEventComponent
  },
  {
    path: 'app/my-events',
    component: MyEventsComponent
  },
  {
    path: 'app/map-view',
    component: MapComponent
  }
];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
