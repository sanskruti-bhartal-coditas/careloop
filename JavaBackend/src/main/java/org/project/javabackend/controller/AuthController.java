package org.project.javabackend.controller;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import lombok.RequiredArgsConstructor;
import org.project.javabackend.dto.response.AccessTokenResponseDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.dto.request.OtpRequest;
import org.project.javabackend.dto.request.VerifyRequestDto;
import org.project.javabackend.dto.response.LoginResponseDto;
import org.project.javabackend.service.AuthService;
import org.project.javabackend.service.RefreshTokenService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/auth")
public class AuthController {

    private final AuthService authService;
    private final RefreshTokenService refreshTokenService;


    @PostMapping("/request-otp")
    public ResponseEntity<GenericResponse> requestOtp(@Valid @RequestBody OtpRequest otpRequestDto) {

        GenericResponse body = authService.requestOtp(otpRequestDto);
        return ResponseEntity.ok(body);
    }

    // login
    @PostMapping("/verify-otp")
    public ResponseEntity<LoginResponseDto> verifyOtp(@Valid @RequestBody VerifyRequestDto verifyRequestDto) {

        LoginResponseDto body = authService.validateLogin(verifyRequestDto);
        return ResponseEntity.ok(body);
    }


    @DeleteMapping("/logout")
    public ResponseEntity<GenericResponse> logout(){
        return ResponseEntity.status(HttpStatus.NO_CONTENT).body(authService.logout());
    }


    // refresh token
    @GetMapping("/refresh/{token}")
    public ResponseEntity<AccessTokenResponseDto> getAccessToken(@NotBlank @PathVariable String token){
        return ResponseEntity.ok(refreshTokenService.refresh(token));
    }

}
