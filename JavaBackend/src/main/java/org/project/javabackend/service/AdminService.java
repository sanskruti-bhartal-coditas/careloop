package org.project.javabackend.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.dto.request.AccountRequestDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.entity.User;
import org.project.javabackend.exception.CustomException;
import org.project.javabackend.repo.UserRepo;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@Slf4j
@RequiredArgsConstructor
@Transactional
public class AdminService {

    private final UserService userService;
    private final UserRepo userRepo;

    public GenericResponse createAccount(AccountRequestDto accountRequestDto) {

        User checkUser = userService.getByEmail(accountRequestDto.email());

        if(checkUser!=null){
            throw new CustomException(HttpStatus.BAD_REQUEST,"user already exist with the same email");
        }

        User user = User.builder()
                .email(accountRequestDto.email())
                .role(accountRequestDto.role())
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();

        try {
            userService.saveUser(user);
        } catch (Exception e) {
            log.error(e.getMessage());
            throw new CustomException(HttpStatus.INTERNAL_SERVER_ERROR,"internal server error");
        }

        return new GenericResponse(HttpStatus.OK,"new user is created successfully");
    }

    public GenericResponse deleteAccount(Long id) {
        User user = userRepo.findById(id).orElseThrow(()-> new CustomException(HttpStatus.BAD_REQUEST,"provided user id is invalid or that user not exist"));
        userRepo.delete(user);
        return new GenericResponse(HttpStatus.NO_CONTENT,"user deleted successfully");
    }
}
