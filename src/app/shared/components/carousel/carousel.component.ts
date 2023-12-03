import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-carousel',
  templateUrl: './carousel.component.html',
  styleUrls: ['./carousel.component.scss']
})
export class CarouselComponent implements OnInit {

  public indicator: boolean = true;
  public controls: boolean = true;
  @Input() public autoSlide: boolean = false;
  public slideInterval: number = 3000;
  public selectedIndex: number = 0;
  public images = [
    { src: '../../../../assets/imgs/Noticias-01-1.jpg' },
    { src: '../../../../assets/imgs/JARDINERIA_2_5.jpg' },
    { src: '../../../../assets/imgs/1140-green-thumb-esp.jpg' },
    { src: '../../../../assets/imgs/jardineria-ecologica_9994f7f8_230331125840_1280x720.jpg' }
  ];

  ngOnInit(): void {
    if(this.autoSlide){
      this.autoSlideImage();
    }
  }

  public autoSlideImage():void{

    setInterval(() => {
      this.nextClick();
    }, this.slideInterval);
  }

  public selectedImage(index: number):void {
    this.selectedIndex = index;
  }

  public prevClick():void{

    if(this.selectedIndex === 0){
      this.selectedIndex = this.images.length - 1;
    } else{
      this.selectedIndex--;
    }
  }

  public nextClick():void{
    if(this.selectedIndex === this.images.length - 1){
      this.selectedIndex = 0;
    } else{
      this.selectedIndex++;
    }
  }

}
