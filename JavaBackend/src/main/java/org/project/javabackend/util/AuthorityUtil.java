package org.project.javabackend.util;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.entity.User;
import org.project.javabackend.exception.CustomException;
import org.project.javabackend.service.UserService;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class AuthorityUtil {

    private final UserService userService;

    public User checkUser(){
        try {
            User user = userService.getUser(SecurityContextHolder.getContext().getAuthentication().getName());
            log.info("checking if the user is a manager or not");
            return user;
        } catch (RuntimeException e) {
            throw new CustomException(HttpStatus.UNAUTHORIZED,"please login to access the application");
        }
    }

}
