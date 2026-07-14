package org.project.javabackend.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.entity.User;
import org.project.javabackend.exception.CustomException;
import org.project.javabackend.repo.UserRepo;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class UserService implements UserDetailsService {

    private final UserRepo userRepo;

    public User getByEmail(String email){
        return userRepo.findByEmail(email);
    }

    public User getUser(String email){
        User user = userRepo.findByEmail(email);
        if(user ==null) throw new CustomException(HttpStatus.NOT_FOUND,"user not found");
        return user;
    }

    @Override
    public User loadUserByUsername(String username) throws UsernameNotFoundException {
        return userRepo.findByEmail(username);
    }

    public void saveUser(User user) {
        userRepo.save(user);
    }
}
