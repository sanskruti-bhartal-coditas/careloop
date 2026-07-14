package org.project.javabackend.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.project.javabackend.dto.request.GenericResponse;
import org.project.javabackend.dto.request.OtpRequest;
import org.project.javabackend.dto.request.VerifyRequestDto;
import org.project.javabackend.service.AuthService;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/auth")
public class AuthController {

    private final AuthService authService;


    @PostMapping("/request-otp")
    public GenericResponse requestOtp(@Valid @RequestBody OtpRequest otpRequestDto) {

        GenericResponse body = authService.requestOtp(otpRequestDto);
        return null;
    }

    // login
    @PostMapping("/verify-otp")
    public GenericResponse verifyOtp(@Valid @RequestBody VerifyRequestDto verifyRequestDto) {

        GenericResponse body = authService.validateLogin(verifyRequestDto);
        return null;
    }


//    @PostMapping("/logout")


    // refresh token


}
