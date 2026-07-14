package org.project.javabackend.service;


import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.project.javabackend.dto.response.AccessTokenResponseDto;
import org.project.javabackend.dto.response.GenericResponse;
import org.project.javabackend.entity.RefreshToken;
import org.project.javabackend.entity.User;
import org.project.javabackend.exception.CustomException;
import org.project.javabackend.repo.RefreshTokenRepo;
import org.project.javabackend.util.JwtUtil;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
@Transactional
@RequiredArgsConstructor
@Slf4j
public class RefreshTokenService {

    private final RefreshTokenRepo refreshTokenRepository;
    private final org.project.javabackend.util.JwtUtil jwtUtil;


    public String createRefreshToken(User user) {
        RefreshToken token = new RefreshToken();
        token.setToken(UUID.randomUUID().toString());
        token.setUser(user);
        token.setExpiryDate(LocalDateTime.now().plusDays(1));

        refreshTokenRepository.save(token);
        return token.getToken();
    }

    public AccessTokenResponseDto refresh(String refreshToken) {

        RefreshToken token = refreshTokenRepository.findById(refreshToken)
                .orElseThrow(()-> new CustomException(HttpStatus.BAD_REQUEST,"Invalid Token"));

        User user = token.getUser();

        if (token.getExpiryDate().isBefore(LocalDateTime.now())) {
            throw new RuntimeException("Expired");
        }
        String newAccess = jwtUtil.generateToken(user.getEmail());
        log.info("refreshing the token with the id : {}",newAccess);
        return new AccessTokenResponseDto(newAccess);
    }

    public List<RefreshToken> getToken(User user) {
        return refreshTokenRepository.findAllByUser(user).orElseThrow(()-> new CustomException(HttpStatus.NOT_FOUND, " no token found to delete"));
    }

    public String delete(List<RefreshToken> refreshTokenList) {
        refreshTokenRepository.deleteAll(refreshTokenList);
        return "the logout successful";
    }
}
