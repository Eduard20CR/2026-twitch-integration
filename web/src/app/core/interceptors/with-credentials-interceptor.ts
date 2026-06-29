import { HttpInterceptorFn } from '@angular/common/http';

export const withCredentialsInterceptor: HttpInterceptorFn = (req, next) => {
  const cookieReq = req.clone({
    withCredentials: true,
  });

  return next(cookieReq);
};
