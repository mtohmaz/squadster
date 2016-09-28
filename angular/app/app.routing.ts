import { ModuleWithProviders }  from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ListViewComponent }   from './list-view.component';
import { CreateEventComponent } from './create-event.component';
import { MyEventsComponent } from './my-events.component';

const appRoutes: Routes = [
  {
    path: '',
    redirectTo: 'list-view',
    pathMatch: 'full'
  },
  {
    path: 'list-view',
    component: ListViewComponent
  },
  {
    path: 'create-event',
    component: CreateEventComponent
  },
  {
    path: 'my-events',
    component: MyEventsComponent
  }
];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
