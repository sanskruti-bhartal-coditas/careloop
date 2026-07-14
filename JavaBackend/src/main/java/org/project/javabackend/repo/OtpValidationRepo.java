package org.project.javabackend.repo;

import org.project.javabackend.entity.OtpValidation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface OtpValidationRepo extends JpaRepository<OtpValidation,Long> {
    Optional<OtpValidation> findByEmail(String email);
}
