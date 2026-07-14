package org.project.javabackend.service;

import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.dto.request.OtpRequest;
import org.project.javabackend.dto.request.VerifyRequestDto;
import org.project.javabackend.dto.response.LoginResponseDto;
import org.project.javabackend.entity.OtpValidation;
import org.project.javabackend.entity.RefreshToken;
import org.project.javabackend.entity.User;
import org.project.javabackend.exception.CustomException;
import org.project.javabackend.repo.OtpValidationRepo;
import org.project.javabackend.repo.RefreshTokenRepo;
import org.project.javabackend.util.AuthorityUtil;
import org.project.javabackend.util.JwtUtil;
import org.springframework.http.HttpStatus;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;
import java.util.Random;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class AuthService {

    private final UserService userService;
    private final OtpValidationRepo otpValidationRepo;
    private final MailService mailService;
    private final JwtUtil jwtUtil;
    private final RefreshTokenService refreshTokenService;
    private final RefreshTokenRepo refreshTokenRepo;
    private final AuthorityUtil authorityUtil;


    public LoginResponseDto validateLogin(@Valid VerifyRequestDto verifyRequestDto) {

        User user = userService.getUser(verifyRequestDto.email());

        OtpValidation otpValidation = otpValidationRepo.findByEmail(verifyRequestDto.email()).orElseThrow(() -> new CustomException(HttpStatus.BAD_REQUEST, "invalid request"));

        // checking the otp is same
        if (!otpValidation.getOtp().equals(verifyRequestDto.otp())) {
            throw new CustomException(HttpStatus.BAD_REQUEST, "the OTP is invalid");
        }
        // checking the expiration on the otp
        boolean isValid = otpValidation.getExpirationTime().before(new Date());

        if (!isValid) {
            throw new CustomException(HttpStatus.BAD_REQUEST, "the OTP is expired ");
        }

        String accessToken = jwtUtil.generateToken(verifyRequestDto.email());
        String refreshToken = refreshTokenService.createRefreshToken(user);

        return new LoginResponseDto(accessToken, refreshToken);
    }

    public GenericResponse requestOtp(@Valid OtpRequest otpRequestDto) {

        User user = userService.getUser(otpRequestDto.email());

        Integer otpInt = new Random().nextInt(100000, 999999);

        String otp = otpInt.toString();
        mailService.mailSender(otpRequestDto.email(),
                "here is the OTP(one time password) to access the account : " + otp,
                "OTP verification for careLoop");


        OtpValidation otpValidation = otpValidationRepo.findByEmail(otpRequestDto.email()).orElse(null);

        if (otpValidation != null) {
            otpValidation.setOtp(otp);
            otpValidation.setExpirationTime(new Date(System.currentTimeMillis() + 1000 * 60 * 15));
            otpValidation.setValidated(false);
        } else {
            otpValidation = OtpValidation.builder()
                    .email(otpRequestDto.email())
                    .otp(otp)
                    .validated(false)
                    .expirationTime(new Date(System.currentTimeMillis() + 1000 * 60 * 15))
                    .build();
        }
        otpValidationRepo.save(otpValidation);

        return new GenericResponse(HttpStatus.OK, "otp sent successfully");
    }




    public GenericResponse logout() {
        User user =authorityUtil.checkUser();
        String result = refreshTokenService.delete(refreshTokenService.getToken(user));
        return new GenericResponse(HttpStatus.NO_CONTENT,result);
    }
}
