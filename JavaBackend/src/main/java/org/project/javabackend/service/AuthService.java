package org.project.javabackend.service;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.dto.request.GenericResponse;
import org.project.javabackend.dto.request.OtpRequest;
import org.project.javabackend.dto.request.VerifyRequestDto;
import org.project.javabackend.entity.OtpValidation;
import org.project.javabackend.entity.User;
import org.project.javabackend.exception.CustomException;
import org.project.javabackend.repo.OtpValidationRepo;
import org.springframework.http.HttpStatus;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Random;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthService {

    private final UserService userService;
    private final OtpValidationRepo otpValidationRepo;
    private final JavaMailSender javaMailSender;






    public GenericResponse validateLogin(@Valid VerifyRequestDto verifyRequestDto) {


    return null;

    }

    public GenericResponse requestOtp(@Valid OtpRequest otpRequestDto) {

        User user = userService.getUser(otpRequestDto.email());

        Integer otpInt = (Integer) new Random().nextInt(100000,999999);

        String otp = otpInt.toString();

        SimpleMailMessage mailMessage = new SimpleMailMessage();

        mailMessage.setFrom("mikhel.pottella@coditas.com");
        mailMessage.setTo(otpRequestDto.email());
        mailMessage.setSubject("verification OTP for login");
        mailMessage.setText("this is the otp(one time password) to access the application: "+ otp);

        try{
            javaMailSender.send(mailMessage);
        } catch (RuntimeException e) {
            log.error(e.getMessage());
            throw new CustomException(HttpStatus.INTERNAL_SERVER_ERROR,"something went wrong");
        }

        OtpValidation otpValidation = OtpValidation.builder()
                .email(otpRequestDto.email())
                .otp(otp)
                .validated(false)
                .expirationTime(LocalDateTime.now().plusMinutes(15))
                .build();

        otpValidationRepo.save(otpValidation);

        return new GenericResponse(HttpStatus.OK,"otp sent successfully");
    }
}
