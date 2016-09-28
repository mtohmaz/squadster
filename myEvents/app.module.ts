import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { AppComponent }  from './app.component';
import { MyEventDetailComponent } from './myEventDetail.component';
@NgModule({
  imports: [
    BrowserModule,
    FormsModule
  ],
  declarations: [
    AppComponent,
    MyEventDetailComponent
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
