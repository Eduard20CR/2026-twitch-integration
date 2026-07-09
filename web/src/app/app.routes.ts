import { Routes } from '@angular/router';
import { isLoggedInGuard } from './core/guards/is-logged-in-guard';

export const routes: Routes = [
    {
        path: '',
        loadChildren: () =>
            import('./modules/home/home.routes')
                .then(m => m.HOME_ROUTES)
    },
    {
        path: 'app',
        canActivateChild: [isLoggedInGuard],
        loadChildren: () =>
            import('./modules/game/game.routes')
                .then(m => m.GAME_ROUTES)
    },
    {
        path: 'profile',
        canActivateChild: [isLoggedInGuard],
        loadChildren: () =>
            import('./modules/profile/profile.routes')
                .then(m => m.PROFILE_ROUTES)
    }
];
