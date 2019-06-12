import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event,ai_settings,screen,ship,bullets):
    #每个“如果”，只对应一个事件!
    if event.key==pygame.K_SPACE and len(bullets)<ai_settings.bullets_allowed:
        fire_bullet(ai_settings,screen,ship,bullets)
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key==pygame.K_ESCAPE:
        sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    # if len(bullets)<ai_settings.bullets_allowed:
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)


def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
          check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
           check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN and not stats.game_active:
            mouse_x,mouse_y=pygame.mouse.get_pos()#返回元组,赋给x，y两个变量
            pygame.mouse.set_visible(False)
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)


def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    if play_button.rect.collidepoint(mouse_x,mouse_y):
        ai_settings.initialize_dynamic_settings()
        stats.game_active=True
        stats.reset_stats()#只有这个的话，下面不写，那么一开始飞船就损失一条命，因为直接调用hit_ship自动减一条命

        sb.prep_score()
        sb.prep_high_score()#没有括号的话不执行函数。！！！！！！！！！！！
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)#Group的方法,自动根据每个alien的rect属性绘制在screen上
    sb.show_score()
    if not stats.game_active:
        pygame.mouse.set_visible(True)
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()  #自动调用每个bullet的update
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)


def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    for aliens in collisions.values():
        stats.score+=ai_settings.alien_points*len(aliens)
        sb.prep_score()
    check_high_score(stats,sb)
    if len(aliens) ==0:
        bullets.empty()##############一定需要吗？？？？？？？？？？？？
        ai_settings.increase_speed()
        stats.level+=1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)


def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()


def create_fleet(ai_settings,screen,ship,aliens):
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings, ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)



def get_number_aliens_x(ai_settings,alien_width):
    available_space_x=ai_settings.screen_width-2*alien_width
    number_aliens_x=int(available_space_x/(2*alien_width))
    return number_aliens_x


def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(2*alien_height))
    return  number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien=Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    if stats.ships_left>0:
        stats.ships_left-=1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(1)#暂停
    else:stats.game_active=False

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
            break

def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)#改变y
    aliens.update()#改变x
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)