import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ListViewComponent }   from './list-view.component';
import { CreateEventComponent } from './create-event.component';
import { MyEventsComponent } from './my-events.component';
import { LogInComponent } from './log-in.component';

const appRoutes: Routes = [
  {
    path: '',
    redirectTo: 'app/list-view',
    pathMatch: 'full'
  },
  {
    path: 'log-in',
    component: LogInComponent
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
  }
];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
