import numpy as np
import scipy.fftpack as fft

class MagneticTransform:
    def __init__(self, data, dx, dy):
        """
        Initialize the Magnetic Transform library.
        
        Parameters:
        data : 2D numpy array
            Magnetic field data.
        dx : float
            Grid spacing in the X direction.
        dy : float
            Grid spacing in the Y direction.
        """
        self.data = data
        self.dx = dx
        self.dy = dy
        self.nx, self.ny = data.shape
        self.kx, self.ky = self.compute_wavenumbers()
    
    def compute_wavenumbers(self):
        """Compute wavenumber arrays for Fourier domain calculations."""
        kx = fft.fftfreq(self.nx, d=self.dx) * 2 * np.pi
        ky = fft.fftfreq(self.ny, d=self.dy) * 2 * np.pi
        KX, KY = np.meshgrid(kx, ky, indexing='ij')
        return KX, KY
    
    def upward_continuation(self, h):
        """Perform upward continuation to height h."""
        k = np.sqrt(self.kx**2 + self.ky**2)
        k[0, 0] = 1  # Avoid division by zero
        data_ft = fft.fft2(self.data)
        continuation_filter = np.exp(-h * k)
        data_continued = fft.ifft2(data_ft * continuation_filter).real
        return data_continued
    
    def vertical_derivative(self, order=1):
        """Compute the vertical derivative of the magnetic field."""
        k = np.sqrt(self.kx**2 + self.ky**2)
        k[0, 0] = 1  # Avoid division by zero
        data_ft = fft.fft2(self.data)
        derivative_filter = (1j * k) ** order
        data_derivative = fft.ifft2(data_ft * derivative_filter).real
        return data_derivative
    
    def total_horizontal_gradient(self):
        """Compute the total horizontal gradient (THG) of the magnetic field."""
        data_ft = fft.fft2(self.data)
        dTx = fft.ifft2(data_ft * (1j * self.kx)).real
        dTy = fft.ifft2(data_ft * (1j * self.ky)).real
        THG = np.sqrt(dTx**2 + dTy**2)
        return THG
